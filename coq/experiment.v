From Coq Require Import Reals.
From Interval Require Import Tactic.
From Coquelicot Require Import Coquelicot.
Require Import ZArith.
Require Import Psatz.
Require Import List.
Import ListNotations.
Set Warnings "-ambiguous-paths".

Open Scope R_scope.

(* Define auxiliary functions *)
Definition w (x : R) := sqrt (8 * x + 1).
Definition s (x : R) := (w x - 1)^2 / (4 * (w x + 7)).
Definition s_inv (x : R) := / (s (/ x)).

Definition c (x : R) := (w x + 3)^2 / 16.
Definition d (x : R) := (w x + 3)^2 / (8 * (w x + 1)).

(* Define s_i functions recursively *)
Fixpoint s_i_pos (i : nat) (x : R) : R :=
  match i with
  | O => x
  | S i' => s (s_i_pos i' x)
  end.

Fixpoint s_i_neg (i : nat) (x : R) : R :=
  match i with
  | O => x
  | S i' => s_inv (s_i_neg i' x)
  end.

Definition c_j_pos (j : nat) (x : R) := c (s_i_pos j x).
Definition d_j_pos (j : nat) (x : R) := d (s_i_pos j x).
Definition c_j_neg (j : nat) (x : R) := c (s_i_neg j x).
Definition d_j_neg (j : nat) (x : R) := d (s_i_neg j x).






(* BELOW IS NOT WORKING *)





(* Define P_k and S_k *)
Definition P_k (k : nat) (x : R) : R :=
  match k with
  | O => 1
  | S k' => 
    sum_f_R0 (fun j => 
      prod_f_R0 (fun i => c_j_pos i x - 1) j + 1
    ) k'
  end.

Goal P_k 4 0.58 >= 1.8818013907136901.
Proof.
  unfold P_k, c_j_pos, s_i_pos, c, s.
  interval with (i_prec 1000).
Qed.

Definition S_k (k : nat) (x : R) : R :=
  match k with
  | O => 1
  | S k' => 
    sum_f_R0 (fun j => 
      prod_f_R0 (fun i => d_j_pos i x - 1) j + 1
    ) k'
  end.


Definition Q_l (l : nat) (x : R) : R :=
  match l with
  | O => 0
  | S O => 0
  | S (S l') => 
    sum_f_R0 (fun j => 
      / prod_f_R0 (fun i => c_j_neg (S (S i)) x - 1) (S j)
    ) l'
  end.

Definition T_l (l : nat) (x : R) : R :=
  match l with
  | O => 0
  | S O => 0
  | S (S l') => 
    sum_f_R0 (fun j => 
      / prod_f_R0 (fun i => d_j_neg (S (S i)) x - 1) (S j)
    ) l'
  end.


(* Define M_down *)
Definition M_down (l k : nat) (a b : R) : R :=
  a * (S_k k a + T_l l b) / (P_k k b + Q_l l a).

(* Theorem to prove *)
Theorem M_down_bound : M_down 2 1 0.58 0.58 >= -1000000000000000000000.
Proof.
  unfold M_down, S_k, T_l, P_k, Q_l, c_j_pos, c_j_neg, d_j_pos, d_j_neg, c, d, w.
  interval with (i_prec 1000).
Qed.

(* Step 1: Define the partition of [1/3, 3] *)
Fixpoint interval_partition_aux (start step : R) (n : nat) (acc : list (R * R)) : list (R * R) :=
  match n with
  | O => acc
  | S n' =>
      let a := start + INR n' * step in
      interval_partition_aux start step n' ((a, a + step) :: acc)
  end.

Definition round_nearest (x : R) : Z :=
  let lower := IZR (Int_part x) in (* Integer part of x *)
  let upper := lower + 1 in
  if Rle_dec (x - lower) (upper - x)
  then Int_part x
  else Int_part x + 1%Z.

Definition interval_partition (start end_ step : R) : list (R * R) :=
  let delta := end_ - start in
  let num_steps := Z.to_nat(round_nearest (delta / step)) in
  interval_partition_aux start step num_steps [].

Require Import Reals.
Require Import Psatz.

Open Scope R_scope.

Definition step_size := 2 * (1 / 10) ^ 7.


Definition partition := interval_partition (1 / 3) 3 step_size.


(* Step 2: Evaluate M_down on each subinterval *)
Fixpoint check_intervals (f : R -> R) (intervals : list (R * R)) : bool :=
  match intervals with
  | [] => true
  | (a, b) :: rest =>
    let lower_bound := f a in
    if Rle_dec 0.9999030108006773 lower_bound then
      check_intervals f rest
    else false
  end.

(* Function to compute M_down for specific l, k *)
Definition M54_down (x : R) : R := M_down 5 4 x x.

(* Final proof that M54 is bounded below by 0.9999030108006773 *)
Theorem M54_lower_bound : forall x, (1/3 <= x <= 3)%R -> M54_down x >= 0.9999030108006773.
Proof.
  (* Partition the interval *)
  unfold M54_down.
  intros x Hx.

  (* Use check_intervals with M54 and the partition *)
  simpl.
  apply check_intervals with (f := M54_down) (intervals := partition).

  (* Use interval tactic for each subinterval *)
  interval with (i_prec 1000).
Qed.