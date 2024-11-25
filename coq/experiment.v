From Coq Require Import Reals.
From Interval Require Import Tactic.
From Coquelicot Require Import Coquelicot.
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
      prod_f_R0 (fun i => d_j (Z.of_nat i) x - 1) j + 1
    ) k'
  end.


(* Define Q_l and T_k *)
Definition Q_l (l : nat) (x : R) : R :=
  match l with
  | O => 0
  | S O => 0
  | S (S l') => 
    sum_f_R0 (fun j => 
      / prod_f_R0 (fun i => c_j (Z.opp (Z.of_nat (S i))) x - 1) (S j)
    ) l'
  end.

Definition T_l (l : nat) (x : R) : R :=
  match l with
  | O => 0
  | S O => 0
  | S (S l') => 
    sum_f_R0 (fun j => 
      / prod_f_R0 (fun i => d_j (Z.opp (Z.of_nat (S i))) x - 1) (S j)
    ) l'
  end.

(* Define M_down *)
Definition M_down (l k : nat) (a b : R) : R :=
  a * (S_k k a + T_l l b) / (P_k k b + Q_l l a).

(* Theorem to prove *)
Theorem M_down_bound : M_down 2 1 0.58 0.58 >= -1000000000000000000000.
Proof.
  unfold M_down, S_k, T_l, P_k, Q_l, s_i, c_j, d_j, s, c, d, w.
  interval with (i_prec 1000).
Qed.
